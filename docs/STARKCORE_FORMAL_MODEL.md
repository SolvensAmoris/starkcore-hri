# StarkCore Formal Model v1.2

S = (data, policy, history)
policy = (kernel, evolvable, authorities)

kernel = {execution_model, hash_method} # inmutable
evolvable = {rules.delta_max, amendment_policy} # mutable con A

I(S) = sha256(canonical(S))

S1 -> S2 valido si:
exists A: verify_amendment(S1,A) AND hash(S2)==A.to

verify_amendment:
1. sig_ok = A.signature in S1.authorities
2. subset_ok = A.changes subset S1.evolvable
3. kernel_ok = S1.kernel == S2.kernel
4. hash_ok = true (implícito)

U BLOCKED = not exists A
EVOLUTION PASS = all ok
FORK VALIDO = exists A1,A2 distintos validos
