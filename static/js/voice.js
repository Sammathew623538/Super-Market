

(function () {
  const micBtn = document.getElementById('micBtn');
  const input  = document.getElementById('q');
  const form   = document.getElementById('searchForm');

  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {
    console.warn('SpeechRecognition not supported');
    micBtn.disabled = true;
    micBtn.title = 'Voice not supported in this browser';
    return;
  }

  const rec = new SR();
  rec.lang = 'en-IN';         // or 'en-IN'
  rec.interimResults = true;  // show live text while speaking
  rec.maxAlternatives = 1;
  let listening = false;

  function start() {
    try { rec.start(); listening = true; micBtn.classList.add('listening'); }
    catch(e){ /* multiple start calls throw; ignore */ }
  }
  function stop() { rec.stop(); listening = false; micBtn.classList.remove('listening'); }

  micBtn.addEventListener('click', () => listening ? stop() : start());

  // Populate text live
  let finalTranscript = '';
  rec.onresult = (e) => {
    let interim = '';
    for (let i = e.resultIndex; i < e.results.length; i++) {
      const t = e.results[i][0].transcript;
      if (e.results[i].isFinal) finalTranscript += t + ' ';
      else interim += t;
    }
    input.value = (finalTranscript + interim).trim();
  };

  // On final end, auto-submit if we have something
  rec.onend = () => {
    listening = false; micBtn.classList.remove('listening');
    if (input.value.trim().length > 0) form.submit();
  };

  rec.onerror = (e) => {
    console.error('Speech error:', e.error);
    micBtn.classList.remove('listening');
    if (e.error === 'not-allowed' || e.error === 'service-not-allowed') {
      alert('Microphone permission denied. Enable mic in browser settings.');
    }
  };
})();
