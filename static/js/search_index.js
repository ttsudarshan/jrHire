document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[type="text"]');
    const jobListings = document.querySelector('.max-w-4xl.mx-auto.space-y-4.p-4');
    let timeoutId;

    function setLoadingState(isLoading) {
        if (isLoading) {
            jobListings.innerHTML = `
                <div class="text-center py-8">
                    <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-gray-300 border-t-blue-600"></div>
                    <p class="mt-2 text-gray-600">Searching...</p>
                </div>
            `;
        }
    }

    function timeSince(date) {
        if (!date) return "No date provided";
        
        // Convert date string to Date object if it's a string
        const givenDate = typeof date === 'string' ? new Date(date) : date;
        const now = new Date();
        
        const secondsPast = Math.floor((now - givenDate) / 1000);
        
        if (secondsPast < 60) {
            return 'less than a minute ago';
        }
        if (secondsPast < 3600) {
            const minutes = Math.floor(secondsPast / 60);
            return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        }
        if (secondsPast < 86400) {
            const hours = Math.floor(secondsPast / 3600);
            return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        }
        if (secondsPast < 604800) {
            const days = Math.floor(secondsPast / 86400);
            return `${days} day${days > 1 ? 's' : ''} ago`;
        }
        if (secondsPast < 2592000) {
            const weeks = Math.floor(secondsPast / 604800);
            return `${weeks} week${weeks > 1 ? 's' : ''} ago`;
        }
        if (secondsPast < 31536000) {
            const months = Math.floor(secondsPast / 2592000);
            return `${months} month${months > 1 ? 's' : ''} ago`;
        }
        const years = Math.floor(secondsPast / 31536000);
        return `${years} year${years > 1 ? 's' : ''} ago`;
    }

    function renderJobs(jobs) {
        jobListings.innerHTML = '';
        
        if (jobs.length === 0) {
            jobListings.innerHTML = `
                <div class="text-center py-8 text-gray-500">
                    <p>No jobs found matching your search</p>
                </div>
            `;
            return;
        }

        jobs.forEach(job => {
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
                                        <span class="font-medium text-gray-700">${job.company_name}</span>
                                        <span class="bg-gradient-to-r from-yellow-100 to-yellow-200 text-yellow-800 px-2 py-0.5 rounded-full text-xs font-semibold animate-pulse">HOT</span>
                                    </div>
                                    <div class="flex items-center gap-3 mt-2 text-gray-600 text-sm">
                                        <span class="flex items-center gap-1">🌍 ${job.location || ''}</span>
                                        ${job.compensation_per_hour ? 
                                            `<span class="flex items-center gap-1 bg-green-50 px-2 py-1 rounded-full">
                                                💰 ${job.compensation_per_hour} USD/hr
                                            </span>` 
                                            : ''}
                                    </div>
                                </div>
                                <span class="text-gray-500 text-sm bg-gray-50 px-2 py-1 rounded-full">${timeSince(job.created_at)}</span>
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
            jobListings.appendChild(jobElement);
        });

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
    }

    searchInput.addEventListener('input', function(e) {
        clearTimeout(timeoutId);
        const searchQuery = e.target.value.trim();
        
        if (searchQuery === '') {
            location.reload();
            return;
        }

        timeoutId = setTimeout(() => {
            setLoadingState(true);
            fetch(`/api/search-jobs?query=${encodeURIComponent(searchQuery)}`)
                .then(response => response.json())
                .then(jobs => renderJobs(jobs))
                .catch(error => {
                    console.error('Error:', error);
                    jobListings.innerHTML = `
                        <div class="text-center py-8">
                            <p class="text-red-500">An error occurred while searching. Please try again.</p>
                        </div>
                    `;
                });
        }, 300);
    });
});