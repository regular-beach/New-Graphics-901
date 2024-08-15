function expandItem(item) {
    // Add the expanded class to the clicked item
    document.querySelectorAll('.grid-item').forEach(el => el.classList.remove('expanded'));
    item.classList.add('expanded');

    // Show the overlay
    document.getElementById('overlay').classList.add('active');
}

function shrinkAll() {
    // Remove the expanded class from all items
    document.querySelectorAll('.grid-item').forEach(el => el.classList.remove('expanded'));

    // Hide the overlay
    document.getElementById('overlay').classList.remove('active');
}
