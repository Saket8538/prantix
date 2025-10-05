var player;
var video_list
document.onreadystatechange = function () {
    if (document.readyState == 'interactive') {
        player = document.getElementById("player")
        video_list = document.getElementById("video_list")
        
        maintainRatio()
        
        // Prevent navigation on locked videos
        preventLockedVideoAccess()
        
        // Add keyboard navigation
        setupKeyboardNavigation()
    }
}

function maintainRatio() {
    var w = player.clientWidth
    var h = (w * 9) / 16
    console.log({ w, h });
    player.height = h
    video_list.style.maxHeight = h + "px"
}

function preventLockedVideoAccess() {
    // Add click prevention for any locked video links
    document.querySelectorAll('.no-preview').forEach(function(element) {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            alert('Please enroll in this course to access this video.');
            return false;
        });
    });
}

function setupKeyboardNavigation() {
    // Add keyboard shortcuts for video navigation
    document.addEventListener('keydown', function(e) {
        // Left arrow key for previous video
        if (e.key === 'ArrowLeft' && !e.ctrlKey && !e.metaKey) {
            const prevBtn = document.querySelector('.video-nav-controls a[href*="lecture"]:first-child');
            if (prevBtn && !prevBtn.hasAttribute('disabled')) {
                e.preventDefault();
                window.location.href = prevBtn.href;
            }
        }
        // Right arrow key for next video
        if (e.key === 'ArrowRight' && !e.ctrlKey && !e.metaKey) {
            const nextBtn = document.querySelector('.video-nav-controls a[href*="lecture"]:last-child');
            if (nextBtn && !nextBtn.hasAttribute('disabled')) {
                e.preventDefault();
                window.location.href = nextBtn.href;
            }
        }
    });
}

window.onresize = maintainRatio