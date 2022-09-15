pub mod decode;
pub mod utils;


fn main() {
    println!("{}", decode::decode("images/printed.png".to_string()));
    println!("{}", decode::decode("images/printeds.png".to_string()));
    println!("{}", decode::decode("images/printeda.png".to_string()));
}

