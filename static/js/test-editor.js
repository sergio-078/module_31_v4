// Тестовый скрипт для проверки редактора
function checkEditor() {
    console.log('=== ТЕСТ РЕДАКТОРА ===');

    if (typeof CKEDITOR === 'undefined') {
        console.error('❌ CKEditor не загружен');
        return false;
    }

    console.log('✅ CKEditor загружен');

    const editor = CKEDITOR.instances['content-editor'];
    if (!editor) {
        console.error('❌ Редактор не инициализирован');
        return false;
    }

    console.log('✅ Редактор инициализирован');

    // Проверяем основные команды
    const commands = [
        'bold', 'italic', 'underline', 'image', 'flash',
        'link', 'unlink', 'table', 'bulletedlist', 'numberedlist'
    ];

    commands.forEach(cmd => {
        if (editor.getCommand(cmd)) {
            console.log(`✅ ${cmd}: доступен`);
        } else {
            console.log(`❌ ${cmd}: недоступен`);
        }
    });

    return true;
}

// Запускаем проверку
setTimeout(checkEditor, 2000);