
const cards = document.querySelectorAll(".showanim")

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry=> {
        entry.target.classList.toggle("SVGAnimate", entry.isIntersecting)

        entry.target.classList.toggle("show", entry.isIntersecting)
        
        
        if (entry.isIntersecting) observer.unobserve(entry.target)

        })
    },
    {
        threshold: .5,
    }
);

cards.forEach(card => {
    observer.observe(card)
});