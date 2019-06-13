pub fn add_one(x: i32) -> i32 {
    x + 1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(add_one(-2), -1);
        assert_eq!(add_one(-1), 0);
        assert_eq!(add_one(0), 1);
        assert_eq!(add_one(1), 2);
        assert_eq!(add_one(-2), -1);
    }
}
