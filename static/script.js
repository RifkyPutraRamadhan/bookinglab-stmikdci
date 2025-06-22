document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.querySelector('.navbar-toggle');
    const navbarMenu = document.getElementById('navbar-menu');

    function toggleMenu() {
        const isExpanded = toggleButton.getAttribute('aria-expanded') === 'true';
        toggleButton.setAttribute('aria-expanded', !isExpanded);
        navbarMenu.classList.toggle('active');
        toggleButton.classList.toggle('active');
    }

    toggleButton.addEventListener('click', toggleMenu);

    document.addEventListener('click', function (event) {
        const isClickInside = navbarMenu.contains(event.target) || toggleButton.contains(event.target);
        if (!isClickInside && navbarMenu.classList.contains('active')) {
            toggleMenu();
        }
    });

    window.addEventListener('resize', function () {
        if (window.innerWidth > 768 && navbarMenu.classList.contains('active')) {
            toggleMenu();
        }
    });
});

document.getElementById('algorithm').addEventListener('change', function () {
    const quantumGroup = document.getElementById('quantum-group');
    if (this.value === 'rr') {
        quantumGroup.style.display = 'block';
    } else {
        quantumGroup.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('statChart');

    if (ctx) {
        const turnaroundTime = parseFloat(document.querySelector('.stats-numbers p:nth-child(1) .stat-value').textContent);
        const waitingTime = parseFloat(document.querySelector('.stats-numbers p:nth-child(2) .stat-value').textContent);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Turnaround Time', 'Waiting Time'],
                datasets: [{
                    label: 'Waktu (menit)',
                    data: [turnaroundTime, waitingTime],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 99, 132, 0.7)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return context.parsed.y.toFixed(2) + ' menit';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Menit'
                        }
                    }
                }
            }
        });
    }
});

function getColorById(id) {
    const colors = [
        '#4CAF50', '#2196F3', '#FF9800', '#9C27B0',
        '#E91E63', '#3F51B5', '#009688', '#FF5722',
        '#607D8B', '#795548', '#8BC34A', '#00BCD4'
    ];
    return colors[id % colors.length];
}

function renderGanttChart(data) {
    const ganttGrid = document.getElementById('ganttGrid');
    if (!ganttGrid) {
        console.warn("Elemen #ganttGrid tidak ditemukan di HTML.");
        return;
    }

    ganttGrid.innerHTML = "";

    const unitWidth = 5;
    const unitSpacing = 30;

    data.forEach(item => {
        const block = document.createElement("div");
        block.className = "gantt-block";
        const left = item.start * (unitWidth + unitSpacing);
        const width = item.duration * unitWidth + (item.duration - 1) * unitSpacing;
        block.style.left = `${left}px`;
        block.style.width = `${width}px`;
        block.style.backgroundColor = getColorById(item.id);
        block.textContent = `${item.name}`;
        ganttGrid.appendChild(block);
    });
}
