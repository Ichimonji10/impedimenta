use std::sync::{mpsc, Arc, Mutex};
use std::thread;

trait FnBox {
    fn call_box(self: Box<Self>);
}

impl<F> FnBox for F
where
    F: FnOnce(),
{
    fn call_box(self: Box<F>) {
        (*self)()
    }
}

type Job = Box<dyn FnBox + Send + 'static>;

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: mpsc::Sender<Job>,
}

impl ThreadPool {
    /// Create a new ThreadPool.
    ///
    /// `size` is the number of threads in the pool.
    ///
    /// # Panics
    ///
    /// If `size` is zero.
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();
        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::with_capacity(size);
        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool { workers, sender }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        self.sender
            .send(job)
            .expect("Failed to send job to worker.");
    }
}

struct Worker {
    id: usize,
    thread: thread::JoinHandle<()>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let join_handle = thread::spawn(move || loop {
            let job = receiver
                .lock()
                .expect("Failed to acquire lock on receiver.")
                .recv()
                .expect("Failed to acquire job from receiver.");
            println!("Worker {} got a job; executing.", id);
            job.call_box();
        });
        Worker {
            id,
            thread: join_handle,
        }
    }
}
