(function(){
  // Intersection reveal
  const io = ('IntersectionObserver' in window) ? new IntersectionObserver((entries)=>{
    entries.forEach(e=>{
      if(e.isIntersecting){ e.target.classList.add('show'); io.unobserve(e.target); }
    });
  },{threshold: .1}) : null;
  document.querySelectorAll('.reveal').forEach(el=> io && io.observe(el));

  // Auto-dismiss only dismissible alerts (Django messages), not static info boxes
  setTimeout(()=>{
    document.querySelectorAll('.alert.alert-dismissible').forEach(a=>{
      if(a.classList.contains('show')){ a.classList.remove('show'); }
      a.style.display='none';
    });
  }, 4000);

  // Back to top
  const back = document.getElementById('backToTop');
  if(back){
    window.addEventListener('scroll', ()=>{
      if(window.scrollY>250){ back.classList.add('show'); } else { back.classList.remove('show'); }
    });
    back.addEventListener('click', ()=> window.scrollTo({top:0, behavior:'smooth'}));
  }

  // Theme toggle removed per design change request

  // Ripple effect on .ripple or .btn-brand (kept for buttons)
  const addRipple = (e)=>{
    const el = e.currentTarget;
    const rect = el.getBoundingClientRect();
    const span = document.createElement('span');
    span.className = 'r';
    const size = Math.max(rect.width, rect.height);
    span.style.width = span.style.height = size + 'px';
    span.style.left = (e.clientX - rect.left - size/2) + 'px';
    span.style.top = (e.clientY - rect.top - size/2) + 'px';
    el.appendChild(span);
    setTimeout(()=> span.remove(), 600);
  };
  document.querySelectorAll('.ripple, .btn-brand').forEach(btn=>{
    btn.classList.add('ripple');
    btn.addEventListener('click', addRipple);
  });

  // Tilt effect removed as requested

  // Scroll progress bar
  const sp = document.getElementById('scrollProgress');
  if(sp){
    const upd = ()=>{
      const h = document.documentElement;
      const max = h.scrollHeight - h.clientHeight;
      const pct = max>0 ? (h.scrollTop / max) * 100 : 0;
      sp.style.width = pct + '%';
    };
    window.addEventListener('scroll', upd, {passive:true});
    window.addEventListener('resize', upd);
    upd();
  }

  // Navbar compact/shadow on scroll
  const nav = document.querySelector('.prantix-navbar');
  if(nav){
    const navUpd = ()=>{
      if(window.scrollY > 20){ nav.classList.add('navbar-scrolled'); }
      else { nav.classList.remove('navbar-scrolled'); }
    };
    window.addEventListener('scroll', navUpd, {passive:true});
    navUpd();
  }
})();
