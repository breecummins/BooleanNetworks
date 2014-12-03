function [partialorder, algexp] = getalgexp(partialorder,c12,c34)
	
	% Records algebraic expressions at each node and the first two constraints.

	syms A B C D E F G H I J K L M N O P

	algexp = { A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P };
	
	for a = algexp
		assumeAlso(a{1} >0)
	end

	if c12
		assumeAlso( A < C < I < K )
		assumeAlso( D < G < L < O )
		assumeAlso( B < E < J < M )
		assumeAlso( F < H < N < P )
	else
		assumeAlso( A < I < C < K )
		assumeAlso( D < L < G < O )
		assumeAlso( B < J < E < M )
		assumeAlso( F < N < H < P )
	end

	if c34
		assumeAlso( A < D < B < F )
		assumeAlso( C < G < E < H )
		assumeAlso( I < L < J < N )
		assumeAlso( K < O < M < P )
	else
		assumeAlso( A < B < D < F )
		assumeAlso( C < E < G < H )
		assumeAlso( I < J < L < N )
		assumeAlso( K < M < O < P )
    end

    % assumeAlso(E<D)

    partialorder = symboliccomparisons(partialorder,algexp);
end

