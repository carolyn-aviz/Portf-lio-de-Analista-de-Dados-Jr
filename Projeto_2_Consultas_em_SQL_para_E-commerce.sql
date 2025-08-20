-- Criação da tabela de vendas com restrições e índices
CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    cliente VARCHAR(50) NOT NULL, 
    produto VARCHAR(50) NOT NULL, 
    categoria VARCHAR(50) NOT NULL, 
    quantidade INT NOT NULL CHECK (quantidade > 0), -- Restrição para quantidade positiva
    valor DECIMAL(10,2) NOT NULL CHECK (valor >= 0), -- Restrição para valor não negativo
    data DATE NOT NULL -- 
);

-- Índices para otimizar consultas
CREATE INDEX idx_vendas_produto ON vendas (produto);
CREATE INDEX idx_vendas_cliente ON vendas (cliente);
CREATE INDEX idx_vendas_data ON vendas (data);

-- Top 5 produtos mais vendidos (com categoria e ordenação secundária)
SELECT 
    v.produto, 
    v.categoria, 
    SUM(v.quantidade) AS total_vendido
FROM vendas v
GROUP BY v.produto, v.categoria
ORDER BY total_vendido DESC, v.produto ASC -- Ordenação secundária por nome do produto
LIMIT 5;

-- Receita mensal com formatação mais legível
SELECT 
    TO_CHAR(DATE_TRUNC('month', data), 'YYYY-MM') AS mes, 
    SUM(valor) AS receita
FROM vendas
GROUP BY DATE_TRUNC('month', data)
ORDER BY DATE_TRUNC('month', data);

-- Clientes mais valiosos com número de compras
SELECT 
    cliente, 
    COUNT(*) AS numero_compras, 
    SUM(valor) AS total_gasto,
    RANK() OVER (ORDER BY SUM(valor) DESC) AS ranking -- Adiciona ranking para lidar com empates
FROM vendas
GROUP BY cliente
ORDER BY total_gasto DESC
LIMIT 5;
