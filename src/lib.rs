pub mod decode;
pub mod utils;

#[cfg(test)]
mod tests {
    use crate::decode;

    #[test]
    fn works() {
        assert_eq!(decode::decode("images/printed.png".to_string()), "hello tomas");
    }
}