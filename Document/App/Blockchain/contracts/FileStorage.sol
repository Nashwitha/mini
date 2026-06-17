// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FileStorage {

    struct FileRecord {
        string fileHash;
        uint256 timestamp;
        address uploader;
    }

    mapping(string => FileRecord) public files;

    event FileStored(string fileHash, address uploader, uint256 time);

    function storeFile(string memory _fileHash) public {

        require(bytes(files[_fileHash].fileHash).length == 0, "File already exists");

        files[_fileHash] = FileRecord(
            _fileHash,
            block.timestamp,
            msg.sender
        );

        emit FileStored(_fileHash, msg.sender, block.timestamp);
    }

    function verifyFile(string memory _fileHash) public view returns(bool){

        if(bytes(files[_fileHash].fileHash).length > 0){
            return true;
        }

        return false;
    }
}