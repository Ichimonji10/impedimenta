// From: http://www.electronicdesign.com/industrial/rust-and-spark-software-reliability-everyone

fn main() {
    let mut v: Vec<i32> = Vec::new();
    v.push(40);
    {
        let mut v2: &Vec<i32> = &mut v;
        v2[0] += 1; // comment out to let program run
    }
    v[0] = v[0] + 1;
    println!("{}", v[0]);
}
