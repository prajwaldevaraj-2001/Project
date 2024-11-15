export const fetchInventory = async () => {
    const response = await fetch('/inventory');
    return response.json();
};

export const addItem = async (item) => {
    const response = await fetch('/inventory', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(item),
    });
    return response.json();
};
