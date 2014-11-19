def repeatingLoop(pattern):
    N=len(pattern)
    if len(set(pattern)) == N:
        return False
    else:
        for n in range(1,N/2):
            if pattern[N-n:N] == pattern[N-2*n:N-n]:
                return True
        return False

if __name__ == '__main__':
    pattern = [2,3,7,8,9,10,8,9,10,8,9,10]
    print(repeatingLoop(pattern))
    pattern = [2,3,7,8,8]
    print(repeatingLoop(pattern))
    pattern = [4,9,7,4]
    print(repeatingLoop(pattern))
