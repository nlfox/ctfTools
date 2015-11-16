<?php

class Diff
{
    public $path;
    public $fileArr;

    public function __construct($path)
    {
        $this->path = $path;
        $this->fileArr = [];
    }

    public function scan(&$arr, $path)
    {
        $files = scandir($path);
        foreach ($files as $file) {
            if ($file != '.' and $file != '..') {
                if (is_file($path . '/' . $file)) {
                    $arr[$file] = md5_file($path . '/' . $file);
                } else {
                    $this->scan($arr[$file], $path . '/' . $file);
                }
            }
        }
    }

    public function getMd5()
    {
        $this->scan($this->fileArr, $this->path);
        return $this->fileArr;
    }

    public function save()
    {
        file_put_contents('checksum' . time() . '.txt', json_encode($this->fileArr));
    }


}

function arrayRecursiveDiff($aArray1, $aArray2)
{
    $aReturn = array();
    foreach ($aArray1 as $mKey => $mValue) {
        if (array_key_exists($mKey, $aArray2)) {
            if (is_array($mValue)) {
                $aRecursiveDiff = arrayRecursiveDiff($mValue, $aArray2[$mKey]);
                if (count($aRecursiveDiff)) {
                    $aReturn[$mKey] = $aRecursiveDiff;
                }
            } else {
                if ($mValue != $aArray2[$mKey]) {
                    $aReturn[$mKey] = $mValue;
                }
            }
        } else {
            $aReturn[$mKey] = $mValue;
        }
    }
    return $aReturn;
}

$oldArr = json_decode(file_get_contents("/var/www/html/checksum1447659829.txt"), true);
$diff = new Diff('/var/www/html/rock/');
$newArr = $diff->getMd5();
$diff->save();
print_r(arrayRecursiveDiff($newArr, $oldArr));
?>
