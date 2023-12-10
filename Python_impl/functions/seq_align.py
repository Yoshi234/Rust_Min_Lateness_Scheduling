'''
based on lecture notes from CSE 3500 - minimum cost string alignment

cost of an alignment M is 
cost(M) = sum(matches,mismatches) + sum(gaps)

suppose you have two strings x=x1,x2,x3,x4,x5,...,xm and 
                             y=y1,y2,y3,y4,y5,...,yn
suppose xm is aligned with a gap - does this mean the remainder of the 
alignment has to correspond to an optimal solution for problem instance
x1,x2,x3,...,xm-1 and y1,y2,y3,...,yn-1?

suppose xm is aligned with yn - does this mean the remainder of the alignment
has to be an optimal solution for instance x1,x2,...,xm-1 and y1,y2,...,yn-1?

base-case: 
    when the ith character in x is aligned with the first character in y, the 
    cost is i*(gap cost)
    the opposite is true as well.
case 1: OPT(i,j) aligns xi and yj 
    pay mismatch/match for xi<->yj and min cost of aligning x1,x2,...,xi-1 and 
    y1,y2,...,yj-1
case 2a: OPT(i,j) leaves xi unmatched
    pay gap xi + min cost of aligning x1,x2,...,xi-1 and y1,y2,...,yj
case 2b: OPT(i,j) leaves yj unmatched
    pay gap yj + min cost of aligning y1,y2,...,yj-1 and x1,x2,...,xi

DP Equation: 
    d = gap cost
    a = mismatch cost

    if i = 0: OPT(i,j) = j*gap_cost
    if j = 0: OPT(i,j) = i*gap_cost
    else: OPT(i,j) = min(mismatch_cost(xi,yj) + OPT(i-1,j-1),
                         gap_cost + OPT(i-1,j), 
                         gap_cost + OPT(i,j-1))
'''
import random

def match_cost(x,y,c):
    if x==y: return 0
    else: return c

class sim_string:
    def __init__(self, x):
        self.x = x
        self.score = -1

    def __len__(self):
        return len(self.x)
    
    def compare_score(self, other, gc=1, mc=1):
        '''
        run optimal string alignment for sim_string=self and sim_string=other
        '''
        OPT = dict()
        m = len(self)
        n = len(other)
    
        for i in range(m+1):
            OPT[(i,0)] = i*gc
        for j in range(n+1):
            OPT[(0,j)] = j*gc

        for i in range(1,m+1):
            for j in range(1,n+1):
                OPT[(i,j)] = min(match_cost(self.x[i-1],other.x[j-1],mc) + OPT[(i-1,j-1)],
                                 gc + OPT[(i-1,j)], 
                                 gc + OPT[(i,j-1)])
        self.score = OPT[(m,n)]
        print("{} v. {} = {}".format(self.x, other.x, self.score))
                                 

def test():
    test_sequences = [sim_string("hello"), 
                      sim_string("goodbye"), 
                      sim_string("there-you-are")]
    random.shuffle(test_sequences)
    input_sequence = sim_string("Hello")
    for seq in test_sequences:
        seq.compare_score(input_sequence)
    s_seqs = sorted(test_sequences, key=lambda item: item.score)
    assert s_seqs[0].x == "hello" 

def main():
    test()
    

if __name__ == "__main__":
    main()
