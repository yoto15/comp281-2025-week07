document.addEventListener('DOMContentLoaded', main);

function main() {
	// เข้าถึง html ผ่านทาง DOM
	const imageFile = document.getElementById('imageFile');
	const imageSrc = document.getElementById('imageSrc');
	const imageDes = document.getElementById('imageDes');
	const imageBefore = document.getElementById('imageBefore');
	const imageAfter = document.getElementById('imageAfter');
	const sendButton = document.getElementById('send');

	const ctxBefore = imageBefore.getContext('2d');
	const ctxAfter = imageAfter.getContext('2d');

	const maxWidth = 800;
	const maxHeight = 600;

	imageFile.addEventListener('change', () => {
		const file = imageFile.files[0];
		console.log(`Selected file: ${file.name}, size: ${file.size} bytes`);
		if (file) {
			const reader = new FileReader();
			reader.onload = function(event) {
				imageSrc.onload = function() {
					let w,h;
					if (imageSrc.width > imageSrc.height) {
						w = maxWidth;
						h = imageSrc.height * (maxWidth / imageSrc.width);
					} else {
						h = maxHeight;
						w = imageSrc.width * (maxHeight / imageSrc.height);
					}
					imageBefore.width = w;
					imageBefore.height = h;
					ctxBefore.clearRect(0, 0, w, h);
					ctxBefore.drawImage(imageSrc, 0, 0, w, h);
				};
				imageSrc.src = event.target.result;
			}
			reader.readAsDataURL(file);
		}
	});

	sendButton.addEventListener('click', () => {
		const backendUrl = '/wp1_backend';
		const data = {
			imageBASE64: imageBefore.toDataURL('image/png').split(',')[1],
			type: 'image/png',
			width: imageBefore.width,
			height: imageBefore.height,
		};
		console.log(`Sending data to backend: `, data);
		fetch(backendUrl, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		})
		.then(response => response.json())
		.then(data => {
			console.log(`Received data from backend: `, data);
			imageDes.onload = function() {
				let w, h;
				w = data.image.width;
				h = data.image.height;
				imageAfter.width = w;
				imageAfter.height = h;
				ctxAfter.clearRect(0, 0, w, h);
				ctxAfter.drawImage(imageDes, 0, 0, w, h);
			}
			imageDes.src = `data:${data.image.type};base64,${data.image.imageBASE64}`;
		});
	});
}