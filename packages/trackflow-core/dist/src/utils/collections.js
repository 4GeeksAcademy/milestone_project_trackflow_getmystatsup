export function filterProductsByWarehouse(products, warehouse) {
    return products.filter((product) => product.warehouse === warehouse);
}
export function filterProductsByCategory(products, category) {
    return products.filter((product) => product.category === category);
}
export function filterLowStockProducts(products) {
    return products.filter((product) => product.stockQuantity <= product.minStockThreshold);
}
export function sortProductsByStock(products, order) {
    const direction = order === "asc" ? 1 : -1;
    return [...products].sort((a, b) => (a.stockQuantity - b.stockQuantity) * direction);
}
export function sortCarriersByReliability(carriers, order) {
    const direction = order === "asc" ? 1 : -1;
    return [...carriers].sort((a, b) => (a.onTimeRate - b.onTimeRate) * direction);
}
