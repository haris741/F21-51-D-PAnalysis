function Pager(tableName, itemsPerPage) {
    'use strict';
    this.tableName = tableName;
    this.itemsPerPage = itemsPerPage;
    this.currentPage = 1;
    this.pages = 0;
    this.inited = false;

    this.showRecords = function (from, to) {
        let rows = document.getElementById(tableName).rows;

        // i starts from 1 to skip table header row
        for (let i = 1; i < rows.length; i++) {
            if (i < from || i > to) {
                rows[i].style.display = 'none';
            } else {
                rows[i].style.display = '';
            }
        }
    };

    this.showPage = function (pageNumber) {
        if (!this.inited) {
            return;
        }

        let oldPageAnchor = document.getElementById('pg' + this.currentPage);
        oldPageAnchor.className = 'pg-normal';
        this.currentPage = pageNumber;
        let newPageAnchor = document.getElementById('pg' + this.currentPage);
        newPageAnchor.className = 'pg-selected';
        let from = (pageNumber - 1) * itemsPerPage + 1;
        let to = from + itemsPerPage - 1;
        this.showRecords(from, to);

        let pgNext = document.querySelector('.pg-next'),
            pgPrev = document.querySelector('.pg-prev');

        if (this.currentPage == this.pages) {
            // pgNext.style.display = 'none';
        } else {
            // pgNext.style.display = '';
        }

        if (this.currentPage === 1) {
            // pgPrev.style.display = 'none';
        } else {
            pgPrev.style.display = '';
        }
    };

    this.prev = function () {
        if (this.currentPage > 1) {
            if(this.currentPage - 1 == 1){
                let element = document.getElementById('pageNavPosition').innerHTML = "";
                pager.showPageNav('pager', 'pageNavPosition');
                this.showPage(this.currentPage -1);
            }else{
                if(this.pages > 5){
                    pager.showPageNavNext('pager', 'pageNavPosition', this.currentPage - 1);
                    this.showPage(this.currentPage - 1);

                }else{
                    let element = document.getElementById('pageNavPosition').innerHTML = "";
                    pager.showPageNav('pager', 'pageNavPosition');
                    this.showPage(this.currentPage - 1);

                }
            }
        }
    };

    this.next = function () {
        if (this.currentPage < this.pages && this.currentPage <= 1) {
            this.showPage(this.currentPage + 1);
        }else if(this.currentPage < this.pages) {
            if(this.pages > 5){
                let element = document.getElementById('pageNavPosition').innerHTML = "";
                pager.showPageNavNext('pager', 'pageNavPosition', this.currentPage + 1);
                this.showPage(this.currentPage + 1);

            }else{
                let element = document.getElementById('pageNavPosition').innerHTML = "";
                pager.showPageNav('pager', 'pageNavPosition');
                this.showPage(this.currentPage + 1);

            }
        }
    };
    this.clickPage = function (page) {
        this.currentPage = page;
        if (this.currentPage < this.pages && this.currentPage <= 1) {
            let element = document.getElementById('pageNavPosition').innerHTML = "";
            pager.showPageNav('pager', 'pageNavPosition');
            this.showPage(this.currentPage);
        }else if(this.currentPage <= this.pages) {
            if(this.pages > 5){
                let element = document.getElementById('pageNavPosition').innerHTML = "";
                pager.showPageNavNext('pager', 'pageNavPosition', this.currentPage);
                this.showPage(this.currentPage);
            }else{
                let element = document.getElementById('pageNavPosition').innerHTML = "";
                pager.showPageNav('pager', 'pageNavPosition');
                this.showPage(this.currentPage);
            }
        }
    };
    this.showPageNavNext = function (pagerName, positionId, pageNext) {
        if (!this.inited) {
            return;
        }
        let element = document.getElementById(positionId),
            pagerHtml = '<span onclick="' + pagerName + '.prev();" class="pg-normal pg-prev"><b class="fa fa-arrow-circle-left" aria-hidden="true"></b></span>';
        let check = 0;
        for (let page = 1; page <= this.pages; page++) {
            if(pageNext + 1 !== this.pages && pageNext !== this.pages && pageNext > 3){
                if(page === 1){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }
                if(pageNext -2 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');" disabled> ... </span>';
                }
                else if(pageNext - 1 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }else if(pageNext === page){
                pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                check++;
                }else if(pageNext + 1 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }else if(pageNext + 2 === page && page !== this.pages){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');" disabled> ... </span>';
                    check++;
                }else if(page === this.pages){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }
            }else if(pageNext + 1 !== this.pages && pageNext !== this.pages && pageNext === 3){
                if(pageNext - 2 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }if(pageNext - 1 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }else if(pageNext === page){
                pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                check++;
                }else if(pageNext + 1 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }else if(pageNext + 2 === page && page !== this.pages){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');" disabled> ... </span>';
                    check++;
                }else if(page === this.pages){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }
            }else if(pageNext + 1 !== this.pages && pageNext !== this.pages){
                if(pageNext - 1 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }else if(pageNext === page){
                pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                check++;
                }else if(pageNext + 1 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }else if(pageNext + 2 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }
                else if(pageNext + 3 === page && page !== this.pages){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');" disabled> ... </span>';
                    check++;
                }else if(page === this.pages){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }
            }else if(pageNext === this.pages){
                if(page === 1){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }
                if(pageNext - 4 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');" disabled> ... </span>';
                    check++;
                }
                if(pageNext - 3 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                }else if(pageNext - 2 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }else if(pageNext - 1 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }else if(pageNext === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }
            }else{
                if(page === 1){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');" disabled> ... </span>';
                    check++;
                }
                if(pageNext - 2 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }else if(pageNext - 1 === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }else if(pageNext === page){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }else if(page === this.pages){
                    pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
                    check++;
                }
            }
        }
        pagerHtml += '<span onclick="' + pagerName + '.next();" class="pg-normal pg-prev"><b class="fa fa-arrow-circle-right" aria-hidden="true" style="line-height:normal;"></b></span>';

        element.innerHTML = pagerHtml;
    };
    this.init = function () {
        let rows = document.getElementById(tableName).rows;
        let records = (rows.length - 1);

        this.pages = Math.ceil(records / itemsPerPage);
        this.inited = true;
    };

    this.showPageNav = function (pagerName, positionId) {
        if (!this.inited) {
            return;
        }
        let element = document.getElementById(positionId),
            pagerHtml = '<span onclick="' + pagerName + '.prev();" class="pg-normal pg-prev"><b class="fa fa-arrow-circle-left" aria-hidden="true"></b></span>';

        var checkPage = 1;
        for (let page = 1; page <= this.pages; page++) {
            console.log("Pages List",this.pages)
            if(checkPage <= 4){
                pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">' + page + '</span>';
            }else if(checkPage === 5 && checkPage !== this.pages){
                pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');"> ... </span>';
            }else if(checkPage === this.pages){
                pagerHtml += '<span id="pg' + page + '" class="pg-normal pg-next" onclick="' + pagerName + '.clickPage(' + page + ');">'+this.pages+'</span>';
            }
            checkPage++;
        }
        pagerHtml += '<span onclick="' + pagerName + '.next();" class="pg-normal pg-prev"><b class="fa fa-arrow-circle-right" aria-hidden="true" style="line-height:normal;"></b></span>';

        element.innerHTML = pagerHtml;
    };
}
let pager = new Pager('pager', 5);

pager.init();
pager.showPageNav('pager', 'pageNavPosition');
pager.showPage(1);