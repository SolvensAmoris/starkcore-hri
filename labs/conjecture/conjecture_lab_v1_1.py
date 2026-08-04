def generate_polynomial_relations():
    candidates=[]
    import itertools
    vars=['n','n**2','n**3','2**n']
    for left,right in itertools.combinations(vars,2):
        for op in ['<','<=','>','>=']:
            expr=f"{left} {op} {right}"
            # fix closure: captura por valor
            def make_fn(l=left,r=right,o=op):
                def fn(n):
                    lv=eval(l,{"n":n}); rv=eval(r,{"n":n})
                    return {"<":lv<rv,"<=":lv<=rv,">":lv>rv,">=":lv>=rv}[o]
                return fn
            candidates.append((expr,make_fn()))
    return candidates
