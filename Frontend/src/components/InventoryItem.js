import React from 'react';

const InventoryItem = ({ item }) => {
    return (
        <div>
            <h2>{item.name}</h2>
            <p>Stock Level: {item.stock_level}</p>
            <p>Reorder Level: {item.reorder_level}</p>
        </div>
    );
};

export default InventoryItem;
