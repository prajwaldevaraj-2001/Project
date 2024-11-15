import React from 'react';
import InventoryItem from './InventoryItem';

const Dashboard = ({ inventory }) => {
    return (
        <div>
            <h1>Inventory Dashboard</h1>
            {inventory.map((item) => (
                <InventoryItem key={item._id} item={item} />
            ))}
        </div>
    );
};

export default Dashboard;
