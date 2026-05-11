// Auto-dismiss flash messages after 4 seconds
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert[data-autohide]').forEach(el => {
    setTimeout(() => el.remove(), 4000);
  });
});
