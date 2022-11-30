USE db_ass
GO

-- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
-- TRIGGER 1a

CREATE OR ALTER TRIGGER trg_UPDATE_HD_GDV
ON BILL_SERVICE
AFTER INSERT
AS
BEGIN
    DECLARE @maKH VARCHAR(8), @ten_goi_DV NVARCHAR(50), @ngay_gio_mua DATETIME;
    SET @maKH = (SELECT BILL_CUSTOMERID FROM inserted);
    SET @ten_goi_DV = (SELECT BILL_PACKAGE_NAME FROM inserted);
    SET @ngay_gio_mua = (SELECT DATE_BUY FROM inserted);
    
    WITH uu_dai_cua_KH AS
    (
        SELECT  CUSTOMERID
                , CTYPE
                , IIF(CTYPE = 1, 100, IIF(CTYPE = 2, 90, IIF(CTYPE = 3 , 85, 80))) AS Giam_gia
                , IIF(CTYPE = 3, 1, IIF(CTYPE = 4, 2, 0)) AS Ngay_them
        FROM CUSTOMER
        WHERE CUSTOMERID = @maKH
    )
    , don_gdv AS
    (
        SELECT hd.BILL_CUSTOMERID
                , hd.BILL_PACKAGE_NAME
                , gdv.PACKAGE_COST AS Gia_goi_dv
                , gdv.NUM_DAYS AS So_ngay_GDV
        FROM BILL_SERVICE hd
        LEFT JOIN PACKAGE gdv ON hd.BILL_PACKAGE_NAME = gdv.PACKAGE_NAME
        WHERE hd.BILL_PACKAGE_NAME = @ten_goi_DV AND hd.DATE_BUY = @ngay_gio_mua
    )
    , thanh_toan_gdv AS
    (
        SELECT  don_gdv.BILL_CUSTOMERID
                , BILL_PACKAGE_NAME
                , Gia_goi_dv*COALESCE(Giam_gia,100)/100 AS Tong_tien
                , (So_ngay_GDV + COALESCE(Ngay_them,0)) AS So_ngay_gdv
        FROM don_gdv 
        LEFT JOIN uu_dai_cua_KH ud ON don_gdv.BILL_CUSTOMERID = ud.CUSTOMERID
    )
    UPDATE BILL_SERVICE
    SET [TOTAL_COST (kVND)] = (SELECT Tong_tien FROM thanh_toan_gdv)
    , USED_DATE = (SELECT So_ngay_gdv FROM thanh_toan_gdv)
    WHERE BILL_CID = @maKH AND BILL_PACKAGE_NAME = @ten_goi_DV AND DATE_BUY = @ngay_gio_mua
END
GO

-- TRIGGER 1b
CREATE OR ALTER TRIGGER trg_INSERT_PHONG_THUE
ON HIRING_ROOM
AFTER INSERT
AS
BEGIN
    DECLARE @maDP CHAR(16);
    SET @maDP = (SELECT HR_BOOKINGID FROM inserted);
    WITH DDP_hien_tai AS
    (
        SELECT  RECEIPT_BOOKINGID
                , RECEIPT_CUSTOMERID
                , RECEIPT_PACKAGE_NAME
                , CHECKIN
                , CHECKOUT
                , DATEDIFF(day, CHECKIN, CHECKOUT) AS So_ngay_dat
        FROM RECEIPT
        WHERE RECEIPT_BOOKINGID = @maDP
    ) 
    , uu_dai_cua_KH AS
    (
        SELECT  CUSTOMERID
                , CTYPE
                , IIF(CTYPE = 1, 100, IIF(CTYPE = 2, 90, IIF(CTYPE = 3 , 85, 80))) AS Giam_gia
        FROM CUSTOMER
    )
    , gia_thue_phong AS
    (
        SELECT  pt.HR_BRANCHID
                , pt.HR_BOOKINGID
                , pt.HR_ROOMID
                , ddp.RECEIPT_CUSTOMERID
                , p.ROOM_TYPEID
                , cn_lp.[PRICE (kVND)] AS Gia_thue_phong
        FROM HIRING_ROOM pt
        JOIN DDP_hien_tai ddp ON pt.HR_BOOKINGID = ddp.RECEIPT_BOOKINGID
        JOIN ROOM p ON pt.HR_BRANCHID = p.ROOM_BRANCHID AND pt.HR_ROOMID = p.ROOMID
        JOIN BRANCH_HAVE_ROOMTYPE cn_lp ON p.ROOM_BRANCHID = cn_lp.BHR_BRANCHID AND p.ROOM_TYPEID = cn_lp.BHR_TYPEID
    )
    , gia_goi_dv AS
    (
        SELECT  DISTINCT ddp.RECEIPT_BOOKINGID
                , ddp.RECEIPT_CUSTOMERID
                , ddp.RECEIPT_PACKAGE_NAME
                , hd.[TOTAL_COST (kVND)] AS Gia_goi_dv
        FROM DDP_hien_tai ddp
        LEFT JOIN BILL_SERVICE hd ON ddp.RECEIPT_PACKAGE_NAME = hd.BILL_PACKAGE_NAME AND ddp.RECEIPT_CUSTOMERID = hd.BILL_CUSTOMERID
    )
    , thong_tin_don AS
    (
        SELECT  ddp.RECEIPT_BOOKINGID
                , gtp.HR_BOOKINGID
                , gtp.Gia_thue_phong
                , COALESCE(ggdv.Gia_goi_dv, 0) AS Gia_goi_dv
                , COALESCE(ud.Giam_gia, 100) AS Giam_gia
                , ddp.So_ngay_dat
        FROM DDP_hien_tai ddp
        LEFT JOIN gia_thue_phong gtp ON ddp.RECEIPT_BOOKINGID = gtp.HR_BOOKINGID
        LEFT JOIN gia_goi_dv ggdv ON ddp.RECEIPT_BOOKINGID = ggdv.RECEIPT_BOOKINGID
        LEFT JOIN uu_dai_cua_KH ud ON ddp.RECEIPT_CUSTOMERID = ud.CUSTOMERID
    )
    , thanh_toan AS
    (
        SELECT ((Gia_thue_phong*So_ngay_dat)*Giam_gia/100 + Gia_goi_dv) AS Tong_tien
        FROM thong_tin_don
    )
    UPDATE RECEIPT 
    SET [Tong_tien (ngan dong)] = (SELECT Tong_tien FROM thanh_toan) 
    WHERE Ma_DP = @maDP
END
GO

-- TRIGGER 1c
CREATE OR ALTER TRIGGER trg_UPDATE_DDP_TINH_TRANG
ON [dbo].[RECEIPT]
   AFTER UPDATE
AS BEGIN
    IF UPDATE (STATUSS)
    BEGIN
        DECLARE @maKH VARCHAR(8), @maDP CHAR(16), @tinhTrangMoi CHAR(1);
		SET @maKH = (SELECT RECEIPT_CUSTOMERID FROM inserted);
		SET @maDP = (SELECT RECEIPT_BOOKINGID FROM inserted);
		SET @tinhTrangMoi = (SELECT STAT FROM inserted);
		
		IF @tinhTrangMoi = '1' -- Da thanh toan
		BEGIN
			WITH DDP_hien_tai AS
			(
				SELECT  RECEIPT_BOOKINGID
						, RECEIPT_CUSTOMERID
						, RECEIPT_PACKAGE_NAME
						, RECEIPT_TOTAL_COST AS Tong_tien
				FROM RECEIPT
				WHERE RECEIPT_BOOKINGID = @maDP
			)
			, gia_goi_dv AS
			(
				SELECT  ddp.RECEIPT_BOOKINGID
						, ddp.RECEIPT_CUSTOMERID
						, ddp.RECEIPT_PACKAGE_NAME
						, gdv.PACKAGE_COST AS Gia_goi_dv
						, gdv.NUM_DAYS AS Ngay_GDV
				FROM DDP_hien_tai ddp
				LEFT JOIN PACKAGE gdv ON ddp.RECEIPT_PACKAGE_NAME = gdv.PACKAGE_NAME
			)
			, thong_tin_don AS
			(
				SELECT  ddp.RECEIPT_BOOKINGID
						, ddp.RECEIPT_CUSTOMERID
						, COALESCE(ddp.Tong_tien, 0) AS Tong_tien
						, COALESCE(ggdv.Gia_goi_dv, 0) AS Gia_goi_dv
				FROM DDP_hien_tai ddp
				LEFT JOIN gia_goi_dv ggdv ON ddp.RECEIPT_BOOKINGID = ggdv.RECEIPT_BOOKINGID
			)
			, diem_moi AS
			(
				SELECT	RECEIPT_CUSTOMERID
                        , Tong_tien
						, Gia_goi_dv
						, (Tong_tien + Gia_goi_dv)/1000000 AS Diem_moi
				FROM thong_tin_don
			)
            , diem_cu AS
            (
                SELECT CUSTOMERID
                        ,POINTS
                FROM CUSTOMER
            )
            , tong_diem AS
            (
                SELECT (Diem_moi + POINTS) AS Tong_diem
                FROM diem_moi 
                JOIN CUSTOMER ON diem_moi.RECEIPT_CUSTOMERID = CUSTOMER.CUSTOMERID  
            )
			UPDATE CUSTOMER SET POINTS = (SELECT Tong_diem FROM tong_diem)
			WHERE CUSTOMERID = @maKH
		END
    END
END
GO
-- UPDATE BOOKTICKET SET STATUSS = 1 WHERE TICKET_ID = 'DP27112022000001'
-- GO

-- TRIGGER 1d
CREATE OR ALTER TRIGGER trg_UPDATE_KH_LOAI
ON [dbo].[CUSTOMER]
   AFTER UPDATE
AS BEGIN
    IF UPDATE (POINTS) 
    BEGIN
        DECLARE @maKH VARCHAR(8);
		SET @maKH = (SELECT CUSTOMERID FROM inserted);
		
		BEGIN
			WITH loai_moi AS
			(
				SELECT IIF(POINTS < 50, 1, IIF(POINTS >= 50 AND POINTS < 100, 2, IIF(POINTS>= 100  AND POINTS < 1000, 3, 4))) AS Loai_Moi
                FROM CUSTOMER
                WHERE CUSTOMERID = @maKH
			)
            UPDATE CUSTOMER SET CTYPE = (SELECT Loai_Moi FROM loai_moi)
            WHERE CUSTOMERID = @maKH
		END
        
    END
END
GO
-- TRIGGER 2
CREATE OR ALTER TRIGGER trg_INSERT_HOA_DON_GDV
ON [dbo].[BILL_SERVICE]
   INSTEAD OF INSERT
AS BEGIN
	DECLARE	@maKH VARCHAR(8) = (SELECT BILL_CUSTOMERID FROM inserted)
			, @tenGoiDV NVARCHAR(50) = (SELECT BILL_PACKAGE_NAME FROM inserted)
			, @ngayBatDauMoi DATETIME = (SELECT START_DAY FROM inserted)
			, @check INT;
    WITH HDGDV_ngay_het_han AS
    (
        SELECT  BILL_PACKAGE_NAME
                , START_DAY
                , DATEADD(YEAR, 1, START_DAY) AS Ngay_het_han
        FROM BILL_SERVICE
        WHERE BILL_CUSTOMERID = @maKH AND BILL_PACKAGE_NAME = @tenGoiDV
    )
    SELECT @check = (SELECT COUNT(*) FROM HDGDV_ngay_het_han WHERE Ngay_het_han >= @ngayBatDauMoi)

    IF @check > 0
    BEGIN
        PRINT 'trg_INSERT_HOA_DON_GDV: Customer cannot buy 2 package with same services!'
    END
    ELSE
    BEGIN
        INSERT INTO BILL_SERVICE SELECT * FROM inserted;
    END
END
GO
