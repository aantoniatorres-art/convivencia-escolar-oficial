document.addEventListener('DOMContentLoaded', () => {
	const themeButtons = document.querySelectorAll('[data-theme-choice]');

	const applyTheme = (theme) => {
		document.documentElement.dataset.theme = theme;
		themeButtons.forEach((button) => {
			button.setAttribute('aria-pressed', String(button.dataset.themeChoice === theme));
		});
	};

	let currentTheme = 'dark';
	try {
		currentTheme = localStorage.getItem('convivencia-theme') || 'dark';
	} catch (error) {
		currentTheme = document.documentElement.dataset.theme || 'dark';
	}
	applyTheme(currentTheme);

	themeButtons.forEach((button) => {
		button.addEventListener('click', () => {
			const theme = button.dataset.themeChoice;
			applyTheme(theme);
			try {
				localStorage.setItem('convivencia-theme', theme);
			} catch (error) {}
		});
	});
});
