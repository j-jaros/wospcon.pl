window.onload = async () => {
    console.log(window.screen.height, window.screen.width)
    const hidden_by_default = document.querySelectorAll('.hidden, .stitle *, .hidden-content')
    hidden_by_default.forEach((el) => scroll_observer.observe(el))
}

const scroll_observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.intersectionRatio >= 0.3) {
            entry.target.classList.replace("hidden", 'visible')
            entry.target.classList.replace("hidden-content", 'hidden-content-show')
        }
    });
}, {threshold: 0.3});

async function countdown() {
    const target = new Date("01/20/2024 10:00")

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

        await new Promise(r => setTimeout(r, 1000))

    }
}

const go_back_arrow = document.getElementById("go_back")
console.log(go_back_arrow)
new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.intersectionRatio < 0.9) {
            go_back_arrow.classList.add('visible')
        } else {
            go_back_arrow.classList.remove('visible')
        }
    });
}, {threshold: 0.9}).observe(document.querySelector("#start>h1"))

countdown()