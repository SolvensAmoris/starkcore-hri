from cosmos_core import AttestedDAG, SeedChannel
import hashlib
def sha256_fake(pkg, ver):
    return hashlib.sha256(f"{pkg}@{ver}".encode()).hexdigest()
def build_dag(chosen, deps):
    ch=SeedChannel()
    dag=AttestedDAG()
    pub={}
    for pkg, ver in chosen:
        h=sha256_fake(pkg, ver)
        node=ch.from_bytes(bytes.fromhex(h[:32]), name=f"{pkg}@{ver}")
        dag.add_node(node.name, metadata={"pkg":pkg,"ver":ver,"ast_node":node})
        pub[node.name]=ch.identity_hash(node)
    for a,b in deps:
        dag.add_edge(f"{a[0]}@{a[1]}", f"{b[0]}@{b[1]}")
    dag.attest(seed_channel=ch, published_hashes=pub)
    return dag.get_execution_order()
