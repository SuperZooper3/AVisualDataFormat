use std::num::ParseIntError;
use image::{Luma};

#[derive(Debug)]
pub enum Data {
    Bar,
    Gap,
}


pub fn is_black(p: &Luma<u16>) -> bool {
    p == &Luma([0])
}

pub fn interpret(data: Vec<Data>) -> String {
    let mut string = String::new();
    for d in data {
        match d {
            Data::Bar => string += "1",
            Data::Gap => string += "0",
        }
    }
    String::from_utf8(decode_binary(&string).expect("Error decoding binary")).expect("Error decoding to UTF-8")
}

fn decode_binary(s: &str) -> Result<Vec<u8>, ParseIntError> {
    (0..s.len())
    .step_by(8)
    .map(|i| u8::from_str_radix(&s[i..i + 8], 2))
        .collect()
}
