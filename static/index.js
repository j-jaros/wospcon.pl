window.onload = async () => {
    const hidden_by_default = document.querySelectorAll('.hidden, .stitle *')
    console.log(hidden_by_default)
    hidden_by_default.forEach((el) => scroll_observer.observe(el))
}


const scroll_observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.intersectionRatio >= 0.5) {
            entry.target.classList.replace("hidden", 'visible-1')
        } else {
            //entry.target.classList.replace("visible", 'hidden')
        }
    });
}, {threshold: 0.5});
history.scrollRestoration = 'manual';

const anchors = document.querySelectorAll('.section-anchor')

let currentSectionAnchor = null;
const anchor_observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            currentSectionAnchor = entry.target;
            console.log(currentSectionAnchor)
            scroll_pos = parseInt(currentSectionAnchor.getAttribute('section'))
            console.log(scroll_pos)
        }
    });
});

anchors.forEach((anchor) => {
    anchor_observer.observe(anchor)
})


// image loop
async function l1() {
    const e = document.getElementById('image1')
    while (true) {
        for (const i of imgs) {
            e.style.backgroundImage = `url("/static/${i}")`
            await new Promise(r => setTimeout(r, 2000))
            console.log('zmieniam')
        }
    }
}

l1()
