import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import Dashboard from './components/Dashboard';

const socket = io.connect('http://localhost:5000');

function App() {
    const [inventory, setInventory] = useState([]);

    useEffect(() => {
        fetch('/inventory')
            .then((res) => res.json())
            .then((data) => setInventory(data));

        socket.on('inventory_update', (item) => {
            setInventory((prevInventory) => [...prevInventory, item]);
        });
    }, []);

    return (
        <div className="App">
            <Dashboard inventory={inventory} />
        </div>
    );
}

export default App;
