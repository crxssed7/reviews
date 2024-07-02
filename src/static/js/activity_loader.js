let activitiesContainer = document.getElementById('activities') // Null at first but reset anyway
let page = 2 // Page 1 results are already loaded on page load


async function sendRequest(page) {
    const { activitiesBaseUrl } = activitiesContainer.dataset
    return await fetch(`${activitiesBaseUrl}${page}`)
}

function handleScroll(event) {
    const maxScroll = activitiesContainer.scrollWidth - activitiesContainer.clientWidth
    if (maxScroll === activitiesContainer.scrollLeft) {
        sendRequest(page)
            .then(response => response.json())
            .then((data) => { handleResponse(data) })
            .catch((err) => { console.log(err) })
    }
}

function buildActivity(activity) {
    const outerDiv = document.createElement('div')
    outerDiv.classList.add('flex', 'flex-col', 'gap-4', 'items-center', 'justify-center', 'h-[200px]', 'min-w-[265px]', 'border-2', 'rounded-md')
    outerDiv.style.borderColor = activity.colour
    outerDiv.style.color = activity.colour

    const statusText = document.createElement('p')
    statusText.classList.add('font-thin', 'tracking-widest', 'uppercase')
    statusText.innerHTML = activity.status
    outerDiv.appendChild(statusText)

    if (activity.progress !== undefined && activity.progress !== null) {
        const progressText = document.createElement('p')
        progressText.classList.add('text-4xl', 'font-bold')
        progressText.innerHTML = activity.progress
        outerDiv.appendChild(progressText)
    }

    const timeText = document.createElement('p')
    timeText.classList.add('font-thin', 'tracking-widest', 'uppercase')
    timeText.innerHTML = activity.createdAt
    outerDiv.appendChild(timeText)

    activitiesContainer.appendChild(outerDiv)
}

function handleResponse(data) {
    const activities = data.activities
    if (activities.length < 50 || activities.length === 0) {
        activitiesContainer.removeEventListener('scroll', handleScroll)
    }

    activities.forEach((activity) => {
        buildActivity(activity)
    })

    page += 1
}

function activityLoader() {
    activitiesContainer = document.getElementById('activities')
    if (activitiesContainer === null) return

    activitiesContainer.addEventListener('scroll', handleScroll)
}

window.addEventListener('load', activityLoader)
