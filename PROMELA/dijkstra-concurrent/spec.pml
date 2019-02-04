#define WORKERS 3

bool inner_wall_doors[WORKERS] = false;
bool outer_wall_doors[WORKERS] = false;
short candidate_id = 0;
short lock_holder = -1;

proctype AcquireReleaseLock(int worker_id) {
    short i = 0;
    bool have_lock = false;
    outer_wall_doors[worker_id] = true;
    do
    ::  have_lock == true ->
        break;
    ::  else ->
        have_lock = false;
        if
        // To acquire the lock, announce your candidacy…
        ::  worker_id != candidate_id ->
            inner_wall_doors[worker_id] = false;
            if
            ::  outer_wall_doors[candidate_id] == false ->
                candidate_id = worker_id;
            ::  else ->
                skip;
            fi
        // …and verify that only you have opened an inner door.
        ::  else ->
            have_lock = true; // maybe
            inner_wall_doors[worker_id] = true;
            i = 0;
            do
            ::  i < WORKERS ->
                if
                ::  i == worker_id ->
                    skip;
                ::  else ->
                    if
                    ::  inner_wall_doors[i] == true ->
                        have_lock = false;
                    ::  else ->
                        skip;
                    fi
                fi
                i++;
            ::  else ->
                break;
            od
        fi
    od

    lock_holder = worker_id;
    assert(lock_holder == worker_id);

    inner_wall_doors[worker_id] = false;
    outer_wall_doors[worker_id] = false;
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
