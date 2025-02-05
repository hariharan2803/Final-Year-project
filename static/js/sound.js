const yogan = document.getElementById('yoga')
const sound = new Audio('/')
yogan.addEventListener('mouseenter',()=>{
    if(sound.paused||sound.ended){
        sound.currentTime = 0
        sound.play()
    }
})

yogan.addEventListener('mouseleave', () => {
    sound.pause();
    sound.currentTime = 0;
});
