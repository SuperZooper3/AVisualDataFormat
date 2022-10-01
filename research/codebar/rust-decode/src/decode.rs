use image::io::Reader as ImageReader;

use crate::utils;

pub fn decode(p: String) -> String {
    let img =  ImageReader::open(p).expect("File not found!");
    let data = img.decode().expect("Error decoding file");
    let pixels = data.into_luma16();

    let mut row = pixels.rows().into_iter().next().expect("No rows to get");
    
    /* Calibrate */
    let mut bar_width = 0;
    loop {
        let pixel = row.next();

        let black: bool;
        match pixel {
            Some(pixel) => black = utils::is_black(pixel),
            None => break
        }
        if black {
            bar_width += 1;
        } else {
            break
        }
    }

    /* Skip calibration */
    for _ in 0..((2*bar_width) - 1) { row.next(); }

    for _ in 0..(3*bar_width) { row.next_back(); }

    /* We do be starting */
    let mut data: Vec<utils::Data> = Vec::new();
    loop {
        let pixel = row.next();
        let black_status: bool;
        match pixel {
            Some(pixel) => black_status = utils::is_black(pixel),
            None => break
        }
        data.push(if black_status { utils::Data::Bar } else { utils::Data::Gap });
        if row.len() >= bar_width - 1 {
            for _ in 0..(bar_width - 1) { row.next(); } 
        } else {
            break;
        }
    }

    return utils::interpret(data);
}
