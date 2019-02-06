#define WORKERS 2

short turn = 0;
bool flags[WORKERS] = false;
short lock_holder = -1;

proctype AcquireReleaseLock(int worker_id) {
    short other_worker_id = 1 - worker_id;
    assert(worker_id == 0 || worker_id == 1);
    assert(other_worker_id == 0 || other_worker_id == 1);
    assert(worker_id != other_worker_id);

    flags[worker_id] = true;
    do
    ::  (turn != worker_id) ->
        flags[other_worker_id] == false;
        turn = worker_id;
    ::  else ->
        break;
    od

    // Critical section would follow this lock acquisition step.
    lock_holder = worker_id;
    assert(lock_holder == worker_id);

    flags[worker_id] = false;
};

init {
    short i = 0;
    do
    ::  i < WORKERS ->
        run AcquireReleaseLock(i);
        i++;
    ::  else ->
        break;
    od
};
