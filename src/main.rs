pub mod decode;
pub mod utils;


fn main() {
    let p = "images/printed.png";
    println!("{}", decode::decode(p.to_string()));
}

