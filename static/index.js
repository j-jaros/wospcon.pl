window.onload = async () => {
    const hidden_by_default = document.querySelectorAll('.hidden, .stitle *, .hidden-content')
    console.log(hidden_by_default)
    hidden_by_default.forEach((el) => scroll_observer.observe(el))
}


const scroll_observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.intersectionRatio >= 0.4) {
            entry.target.classList.replace("hidden", 'visible')
            entry.target.classList.replace("hidden-content", 'hidden-content-show')
        } else {
            //entry.target.classList.replace("visible", 'hidden')
        }
    });
}, {threshold: 0.4});
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


async function countdown() {
    const target = new Date("01/19/2024 10:00")

    const day_holder = document.querySelector("#until .digits td:first-of-type")
    const hour_holder = document.querySelector("#until .digits td:nth-of-type(2)")
    const minutes_holder = document.querySelector("#until .digits td:nth-of-type(3)")
    const seconds_holder = document.querySelector("#until .digits td:nth-of-type(4)")

    while (true) {
        const diff = target - new Date()

        day_holder.textContent = Math.floor(diff / (1000 * 60 * 60 * 24));
        hour_holder.textContent = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        minutes_holder.textContent = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        seconds_holder.textContent = Math.floor((diff % (1000 * 60)) / 1000);

        await new Promise(r=>setTimeout(r, 1000))

    }
}

countdown()