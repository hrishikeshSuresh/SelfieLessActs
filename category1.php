$dir          = 'category1';
$file_display = array('jpg', 'jpeg', 'png', 'gif');
$dir_contents = scandir($dir);
foreach ($dir_contents as $file){
    $file_type = strtolower(end(explode('.', $file)));
    if ($file !== '.' && $file !== '..' && in_array($file_type, $file_display) == true) {
        // < echo '<img src="'. $dir. '/'. $file. '" alt="'. $file. $
    }
}
