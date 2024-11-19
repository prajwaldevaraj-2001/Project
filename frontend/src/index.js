import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import io from 'socket.io-client';

const socket = io("http://localhost:5000");

const App = () => {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/products')
            .then(response => response.json())
            .then(data => setProducts(data));

        socket.on('update', (update) => {
            alert(`Product ${update.id} has low stock!`);
        });

        return () => socket.disconnect();
    }, []);

    return (
        <div>
            <h1>Real-Time Inventory</h1>
            <ul>
                {products.map(product => (
                    <li key={product._id}>
                        {product.name}: {product.stock_level} units
                    </li>
                ))}
            </ul>
        </div>
    );
};

ReactDOM.render(<App />, document.getElementById('root'));
