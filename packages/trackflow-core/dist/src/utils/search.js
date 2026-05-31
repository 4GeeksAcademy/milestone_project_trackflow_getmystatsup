export function findProductBySKU(products, sku) {
    const target = sku.toLowerCase();
    for (const product of products) {
        if (product.sku.toLowerCase() === target) {
            return product;
        }
    }
    return null;
}
export function findShipmentById(shipments, id) {
    for (const shipment of shipments) {
        if (shipment.id === id) {
            return shipment;
        }
    }
    return null;
}
export function binarySearchProductByWeight(sortedProducts, targetWeight) {
    let left = 0;
    let right = sortedProducts.length - 1;
    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        const midWeight = sortedProducts[mid].weightKg;
        if (midWeight === targetWeight) {
            return mid;
        }
        if (midWeight < targetWeight) {
            left = mid + 1;
        }
        else {
            right = mid - 1;
        }
    }
    return -1;
}
