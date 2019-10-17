use std::fs;
use std::io::{Read, Write};
use std::net::TcpListener;
use std::net::TcpStream;

const BIND_TARGET: &str = "127.0.0.1:7878";

fn main() {
    let listener =
        TcpListener::bind(BIND_TARGET).expect(&format!("Failed to bind to {}", BIND_TARGET)[..]);
    for stream in listener.incoming() {
        handle_connection(stream.expect("Failed to open TCP stream."));
    }
}

fn handle_connection(mut stream: TcpStream) {
    // Read request.
    // NOTE: The buffer handling logic sucks, but it's good enough for educational purposes.
    let mut req_buf = [0; 512];
    stream
        .read(&mut req_buf)
        .expect("Failed to read request from TCP stream.");

    // Construct response.
    let (head, body_file) = if req_buf.starts_with(b"GET / HTTP/1.1\r\n") {
        ("HTTP/1.1 200 OK\r\n\r\n", "assets/hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND\r\n\r\n", "assets/404.html")
    };
    let body = fs::read_to_string(body_file).expect(&format!("Failed to read {}", body_file)[..]);
    let response = format!("{}{}", head, body);

    // Send response.
    stream
        .write_all(response.as_bytes())
        .expect("Failed to write response to TCP stream.");
    stream.flush().expect("Failed to flush TCP stream.");
}
