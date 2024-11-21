let currentPage = 1;
let loading = false;

function timeSince(dateString) {
    if (!dateString) return "No date provided";
    const date = new Date(dateString + 'Z');
    const now = new Date();
    const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);
    
    const intervals = [
        { seconds: 31536000, label: 'year' },
        { seconds: 2592000, label: 'month' },
        { seconds: 604800, label: 'week' },
        { seconds: 86400, label: 'day' },
        { seconds: 3600, label: 'hour' },
        { seconds: 60, label: 'minute' }
    ];

    for (let interval of intervals) {
        const count = Math.floor(seconds / interval.seconds);
        if (count >= 1) {
            return `${count} ${interval.label}${count > 1 ? 's' : ''} ago`;
        }
    }
    
    return "less than a minute ago";
}

function isNearBottom() {
    return window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 500;
}

function loadMoreJobs() {
    if (loading) return;
    loading = true;
    currentPage++;

    fetch(`/load_more?page=${currentPage}`)
        .then(response => response.json())
        .then(jobs => {
            const container = document.querySelector('.max-w-4xl.mx-auto.space-y-4.p-4');
            
            if (!jobs || jobs.length === 0) {
                loading = false;
                return;
            }
            jobs.forEach(job => {
                const formattedDate = timeSince(job.created_at);
                const jobElement = document.createElement('a');
                jobElement.href = `/jobs/${job.id}`;
                jobElement.className = 'block';
                jobElement.innerHTML = `
                    <div class="card-container bg-gradient-to-b from-white to-gray-50 rounded-lg p-4 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-gray-100 relative overflow-hidden">
                        <div class="geometric-pattern absolute inset-0 opacity-5"></div>
                        <div class="card-gradient absolute inset-0 opacity-0 pointer-events-none"></div>
                        <div class="flex items-center gap-4 relative z-10">
                            <div class="w-12 h-12 rounded-full flex items-center justify-center shadow-inner" 
                                 style="background: linear-gradient(135deg, ${job.profile_colors}, ${job.profile_colors}dd);">
                                <span class="text-xl font-bold text-white text-shadow">${job.company_name[0]}</span>
                            </div>
                            
                            <div class="flex-grow">
                                <div class="flex justify-between items-start">
                                    <div>
                                        <h2 class="font-bold text-lg text-gray-800 hover:text-blue-600 transition-colors">${job.job_title}</h2>
                                        <div class="flex items-center gap-2 text-sm">
                                            <span class="flex items-center gap-1">🌍 ${job.location || ''}</span>
                                            ${job.compensation_per_hour ? 
                                                `<span class="flex items-center gap-1 bg-green-50 px-2 py-1 rounded-full">
                                                    💰 ${job.compensation_per_hour} USD/hr
                                                </span>` 
                                                : ''}
                                        </div>
                                    </div>
                                    <span class="text-gray-500 text-sm bg-gray-50 px-2 py-1 rounded-full">${formattedDate}</span>
                                </div>
                                ${job.tags ? `
                                <div class="flex flex-wrap gap-2 mt-3">
                                    ${job.tags.split(',').map(tag => 
                                        `<span class="px-3 py-1 rounded-full text-sm bg-gradient-to-r from-green-100 to-blue-100 hover:from-green-200 hover:to-blue-200 transition-all duration-300 border border-transparent hover:border-green-200">
                                            ${tag.trim()}
                                        </span>`
                                    ).join('')}
                                </div>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                `;
                container.appendChild(jobElement);
            });
            loading = false;
    
            // Add mousemove event listeners to new cards
            const cards = document.querySelectorAll('.card-container');
            cards.forEach(card => {
                card.addEventListener('mousemove', (e) => {
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    card.style.setProperty('--mouse-x', `${x}px`);
                    card.style.setProperty('--mouse-y', `${y}px`);
                });
            });
        })
        .catch(error => {
            console.error('Error loading more jobs:', error);
            loading = false;
        });
}

window.addEventListener('scroll', () => {
    if (isNearBottom()) {
        loadMoreJobs();
    }
});