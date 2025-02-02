window.SuperLists = {};
window.SuperLists.initialize = function () {
	$('input[name="text"]').on('keypress', function () {
		$('.has-error').hide();
	});
};
