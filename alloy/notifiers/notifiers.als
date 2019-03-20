/* This Alloy model describes a hypothetical design for an aspect of Killjoy.
 *
 * Killjoy has a watcher process. This watcher process watches units appear,
 * change state, and disappear. When certain events of interest occur, the
 * watcher takes action, and these actions eventually cause notifications (such
 * as emails) to be sent out.
 *
 * When an "interesting" event occurs, the watcher notifies one or more
 * formatters, and each formatter notifies one or more formatters and notifiers.
 * The relationships between the watcher, formatters, and notifiers are defined
 * by an end user. A formatter merely transforms a message given to it, and a
 * notifier takes action, such as sending an email.
 *
 * It is killjoy's job to ensure that the relationships between the watcher,
 * formatters, and notifiers comprise a directed acyclic graph. If the
 * relationships can form a non-DAG, then a single notification can cause an
 * eternal notification loop. This Alloy model describes the logic for ensuring
 * sane DAGs.
 *
 * What defines a DAG? An informal definition is that, from any given node, it
 * is impossible to walk edges and arrive at that same node.
 *
 * How does one verify that a graph is a DAG? A naive approach is to implement
 * the check specified above. While this should work, implementing that check on
 * an actual graph could be computationally expensive. A more elegant solution
 * is, for every node, to recursively walk the "parent" edge and check whether
 * that same node is reachable.
 *
 * This Alloy model informally proves that walking parent edges allows one to
 * verify that a graph is a DAG.
 */

sig WatchRule {
    // A watch rule must reference at least one formatter.
    wr_children: some Formatter
}

/* Concrete implementations could include HTMLFormatter or NullFormatter. */
sig Formatter {
    // A formatter has a parent.
    f_parent: one (WatchRule + Formatter),

    // A formatter references at least one notifier.
    f_children: some (Formatter + Notifier)
}
fact {
    all f: Formatter | f.f_parent = (wr_children.f + f_children.f)
    no f: Formatter | f in f.^f_parent
}

/* Concrete implementations could include IRCNotifier or EmailNotifier. */
sig Notifier {
    // A notifier has a parent.
    n_parent: one Formatter
}
fact {
    all n: Notifier | n.n_parent = f_children.n
}

pred show {}
run show for 3

// A formatter may not reference itself, directly or indirectly.
assert acyclic {no f: Formatter | f in f.^f_children}
check acyclic for 5
