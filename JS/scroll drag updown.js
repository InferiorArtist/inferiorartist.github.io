 //drag up and down script
 const slider = document.querySelector(".scroll");
 let isDown = false;
 let startY;
 let scrollTop;

 slider.addEventListener("mousedown", e => {
   isDown = true;
   slider.classList.add("active");
   startY = e.pageY - slider.offsetTop;
   scrollTop = slider.scrollTop;
 });
 slider.addEventListener("mouseleave", () => {
   isDown = false;
   slider.classList.remove("active");
 });
 slider.addEventListener("mouseup", () => {
   isDown = false;
   slider.classList.remove("active");
 });
 slider.addEventListener("mousemove", e => {
   if (!isDown) return;

   const y = e.pageY - slider.offsetTop;
   const walk = y - startY;
   slider.scrollTop = scrollTop - walk;
 });