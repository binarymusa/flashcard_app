const getApp = document.querySelector('#app');
const getAppqr = document.querySelector('#appshare');

getApp.addEventListener('mouseenter', () => {
    getAppqr.classList.toggle('show');
});

getApp.addEventListener('mouseleave', () => {
    getAppqr.classList.remove('show');
});

document.addEventListener('click', (e) => {
    if (!getApp.contains(e.target)) {
        getAppqr.classList.remove('show');
    }
});