// ============================================================
// ATS site configuration (shared by index.html and index_ro.html)
// GOOGLE_CLIENT_ID: OAuth client (Web) of the Google Cloud project "MFM Quiz Login",
//   shared with the MFM, SFM and TSA sites (same origin https://danpele.github.io);
//   the quizzes require "Sign in with Google" with an ASE account (@ase.ro / @stud.ase.ro).
// QUIZ_SCORES_URL: Google Apps Script web app that verifies the Google token and stores the score
//   (to be created: Google Sheet "ATS 2026/2027 - Scoruri quiz", Apps Script project "ATS Quiz Scores 2026-2027").
//   The ATS quizzes are GRADED (20% of the final grade), so this backend must be configured before the semester.
// ATTENDANCE_FORM_URL / ATTENDANCE_QR_URL: Google Form "ATS 2026/2027 - Prezență / Attendance" and the QR page
//   of the Apps Script project "ATS Prezenta 2026-2027" (ASE accounts only; attendance is 10% of the grade).
// Values starting with 'YOUR_' are treated as not configured: the site then hides the attendance button,
// shows the quizzes without saving scores, and hides the instructor QR access.
// ============================================================
window.ATS_CONFIG = {
    GOOGLE_CLIENT_ID: '1095360272769-rhjjncfor0gumhev6a0l6tnnrnmdrnna.apps.googleusercontent.com',
    ATTENDANCE_FORM_URL: 'https://forms.gle/DwzBoTQYFAfSC9o4A',
    ATTENDANCE_QR_URL: 'https://script.google.com/a/macros/ase.ro/s/AKfycbyGmvyrmv9bofxtCbgRDtvOLER08_GMRj8HIWIm1yKMSvdChTLDto8NFs6SN6q0LtLH/exec',
    // The QR links appear on the site only after one of these accounts signs in with Google
    INSTRUCTORS: ['danpele@ase.ro'],
    QUIZ_SCORES_URL: 'https://script.google.com/macros/s/AKfycbzO7dFt6CZdoVH0-I96tiaDzhumOiMIvSScXoM5kC4SAUJdI_bIEPLYr_v_x6KIPXVA/exec'
};
