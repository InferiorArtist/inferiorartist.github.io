
    console.clear()

const CARD = document.querySelector('.card')

const UPDATE = ({ x, y }) => {
  const BOUNDS = CARD.getBoundingClientRect()
  // Calculate the range between the center and the pointer position.
  const posX = x - BOUNDS.x
  const posY = y - BOUNDS.y
  const ratioX = posX / BOUNDS.width
  const ratioY = posY / BOUNDS.height
  // CARD.style.setProperty('--x', posX)
  // CARD.style.setProperty('--y', posY)
  CARD.style.setProperty('--ratio-x', ratioX)
  CARD.style.setProperty('--ratio-y', ratioY)
  // console.info({ posX, posY })
}

document.body.addEventListener('pointermove', UPDATE)
