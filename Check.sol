// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Check{
    enum status {Fake, Real, Unverified}
    enum typeSen {Sensitive, Unsensitive}

    uint current = 0;
    struct News{
        address publisher;
        uint time;
        status s;
        string link;
        uint t;
    }
    event ReturnValue(uint indexed value);
    uint totalLinks = 0;
    string[20] public lastLinks;
    mapping (string => News) public storeStatus;
    mapping (string => int) public storeVotes;
    mapping (address => uint) public rating;
    mapping (address => uint) public block_list;
    mapping (string => uint) public pending;
    
    function getVotes(string memory link) view public returns (int) {
        return storeVotes[link];
    }
    function addJourno(address a) public {
        rating[a] = 1;
        if(block_list[a] == 0){
            block_list[a] = 0;
        }
    }

    function removeJourno(address a) public {
        delete rating[a];
        block_list[a]++;
    }
    function findPublisher(string memory link) public view returns (address){
        return storeStatus[link].publisher;
    }
    function checkNews(string memory link) public view returns (News memory){
        News memory r = storeStatus[link];
        return r;
    }

    function incRating(address a, uint change) public{
        rating[a] += change;
    }

    function decRating10(address a) public{
        rating[a] /= 10;
    }
    
    function decRating20(address a) public{
        rating[a] /= 20;
    }
    function getBlockCount(address a) public view returns (uint){
        return block_list[a];
    }
    function getRating(address a) public view returns (uint){
        return rating[a];
    }

    function changeRating(address a, uint new_rating) public {
        rating[a] = new_rating;
        if(rating[a] == 0){
            delete rating[a];
            block_list[a]++;
        }
    }
    function addNews(address st, uint time, string memory link, uint t) public returns (string memory){
        if(rating[st] > 0){
            storeStatus[link] = News(st, time, status.Unverified, link, t);
            storeVotes[link] = 0;
            pending[link] = 1;
            lastLinks[totalLinks++] = link;
            totalLinks = totalLinks%20;
            // links.push() = link;
            return "News added successfully";
        }
        else{
            return "Your identity has been revoked. Please register again.";
        }
    }

    function castVote(string memory link, int vote) public returns (uint u){ // 0 : fake, 1 : real, 2 : undecided, 3 : voting_closed
        if(pending[link] != 0){
            storeVotes[link] += vote;
            pending[link]++;
            if(pending[link] >= 10){
                if(storeVotes[link] > 0){
                    pending[link] = 0;
                    storeStatus[link].s = status.Real;
                    rating[storeStatus[link].publisher]++;
                    u = 1;
                }
                else if(storeVotes[link] < 0){
                    pending[link] = 0;
                    storeStatus[link].s = status.Fake;
                    rating[storeStatus[link].publisher] /= 10;
                    if(rating[storeStatus[link].publisher] == 0){
                        removeJourno(storeStatus[link].publisher);
                    }
                    u = 0;
                }
                else{
                    u = 2;
                }
            }
            else{
                u = 2;
            }
        }
        else{
            u = 3;
        }

        emit ReturnValue(u);
    }


    function castVoteU(string memory link, int vote) public{
        if(pending[link] != 0 && storeStatus[link].t == 1){
            storeVotes[link] += vote;
            pending[link]++;
            if(pending[link] > 10){
                if(storeVotes[link] > 0){
                    pending[link] = 0;
                    storeStatus[link].s = status.Real;
                    rating[storeStatus[link].publisher]++;
                }
                else if(storeVotes[link] < 0){
                    pending[link] = 0;
                    storeStatus[link].s = status.Fake;
                    rating[storeStatus[link].publisher] /= 10;
                    if(rating[storeStatus[link].publisher] == 0){
                        removeJourno(storeStatus[link].publisher);
                    }
                }
            }
        }
    }

    function isActive(string memory link) public view returns (bool){
        if(pending[link] > 0){
            return true;
        }
        else{
            return false;
        }
    }
    function last20Links() public view returns (string[20] memory ans){
        ans = lastLinks;
        return ans;
    }
}
