// Скрипт для отладки CKEditor
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM загружен, проверяем CKEditor...');

    // Проверяем наличие CKEditor
    if (typeof CKEDITOR === 'undefined') {
        console.error('CKEditor не загружен!');
        // Пытаемся загрузить вручную
        const script = document.createElement('script');
        script.src = 'https://cdn.ckeditor.com/4.22.1/standard/ckeditor.js';
        script.onload = function() {
            console.log('CKEditor загружен вручную');
            initCKEditor();
        };
        document.head.appendChild(script);
    } else {
        console.log('CKEditor уже загружен');
        setTimeout(initCKEditor, 100);
    }
});

function initCKEditor() {
    console.log('Инициализация CKEditor...');

    try {
        CKEDITOR.replace('content-editor', {
            language: 'ru',
            height: 400,
            toolbar: [
                ['Bold', 'Italic', 'Underline', 'Strike'],
                ['NumberedList', 'BulletedList'],
                ['Link', 'Unlink', 'Image'],
                ['Source']
            ],
            filebrowserUploadUrl: '/ckeditor/upload/',
            filebrowserUploadMethod: 'form'
        });

        console.log('CKEditor инициализирован успешно');
    } catch (error) {
        console.error('Ошибка инициализации CKEditor:', error);
    }
}