byte counter = 0;
byte completed_procs = 0;

active [2] proctype P() {
    byte reg = 0;
    byte i = 0;
    do
    ::  i == 5 ->
        break;
    ::  else ->
        reg = counter;
        reg++;
        counter = reg;
        i++;
    od;
    completed_procs++;
};

active proctype WaitForCompletedProcs() {
    completed_procs == 2;
    printf("counter = %d\n", counter);
    assert(counter <= 10); // true
    assert(counter >= 5); // false
};
