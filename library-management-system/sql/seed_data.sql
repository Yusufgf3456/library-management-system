-- Sample data (for testing and demo purposes)

INSERT INTO books (title, author, isbn, published_year, total_copies, available_copies) VALUES
    -- Dünya klasikleri
    ('Crime and Punishment',         'Fyodor Dostoevsky',          '9780486415871', 1866, 3, 3),
    ('Les Miserables',               'Victor Hugo',                '9780451419439', 1862, 2, 2),
    ('1984',                         'George Orwell',              '9780451524935', 1949, 4, 4),
    ('To Kill a Mockingbird',        'Harper Lee',                 '9780061120084', 1960, 2, 2),
    ('Animal Farm',                  'George Orwell',              '9780451526342', 1945, 1, 1),
    ('The Great Gatsby',             'F. Scott Fitzgerald',        '9780743273565', 1925, 3, 3),
    ('Pride and Prejudice',          'Jane Austen',                '9780141439518', 1813, 2, 2),
    ('The Little Prince',            'Antoine de Saint-Exupery',   '9780156012195', 1943, 5, 5),
    ('The Alchemist',                'Paulo Coelho',               '9780061122415', 1988, 4, 4),
    ('One Hundred Years of Solitude','Gabriel Garcia Marquez',     '9780060883287', 1967, 2, 2),
    ('The Catcher in the Rye',       'J. D. Salinger',             '9780316769488', 1951, 2, 2),
    ('Brave New World',              'Aldous Huxley',              '9780060850524', 1932, 3, 3),
    ('The Hobbit',                   'J. R. R. Tolkien',           '9780547928227', 1937, 3, 3),

    -- Türk edebiyatı
    ('Kurk Mantolu Madonna',         'Sabahattin Ali',             '9789753638029', 1943, 4, 4),
    ('Ince Memed',                   'Yasar Kemal',                '9789750726439', 1955, 3, 3),
    ('Calikusu',                     'Resat Nuri Guntekin',        '9789751031464', 1922, 2, 2),
    ('Tutunamayanlar',               'Oguz Atay',                  '9789754700114', 1972, 2, 2),
    ('Saatleri Ayarlama Enstitusu',  'Ahmet Hamdi Tanpinar',       '9789753638562', 1961, 2, 2),
    ('Benim Adim Kirmizi',           'Orhan Pamuk',                '9789750806469', 1998, 3, 3),
    ('Ask',                          'Elif Safak',                 '9789750718533', 2009, 4, 4),
    ('Serenad',                      'Zulfu Livaneli',             '9789752108233', 2011, 2, 2);

INSERT INTO members (name, email, phone) VALUES
    ('Ahmet Yilmaz',  'ahmet.yilmaz@example.com',  '0532 111 22 33'),
    ('Ayse Demir',    'ayse.demir@example.com',    '0533 222 33 44'),
    ('Mehmet Kaya',   'mehmet.kaya@example.com',   '0534 333 44 55'),
    ('Zeynep Sahin',  'zeynep.sahin@example.com',  '0535 444 55 66'),
    ('Mustafa Celik', 'mustafa.celik@example.com', '0536 555 66 77'),
    ('Elif Aydin',    'elif.aydin@example.com',    '0537 666 77 88'),
    ('Can Ozturk',    'can.ozturk@example.com',    '0538 777 88 99');