import re

def norm(text):
    text = text.strip(); # trim
    text = removeNone(text)
    text = truncLongName(text)
    return text

def removeNone(text):
    newText = text.replace('\n📕 Nome: None.', '').replace( '\n🕙 Última atualização: None.', '').replace( '\n↪️ Situação: None.', '').replace('\n🔈 Tramitação: None.', '').replace(', de autoria de None,', '').replace('Atualização: None.', '')
    return newText

def removeEmoji(text):
    newText = text.replace('📕', '').replace( '🕙', '').replace( '↪️', '').replace('🔈', '').replace('🔗', '').replace('💡', '')
    return newText

def repNameV1(m):
    names = m.group(2).split(', ')

    # mais de um author
    if (len(names) > 1):
        return m.group(1) + names[0] + ' e outros(as)' + m.group(3)

    return m.group(1) + names[0] + m.group(3)

def repNameV2(m):
    names = m.group(2).split(', ')

    firstName = names[0]
    if (len(names) > 1):
        if (len(firstName) > 20):
            nameParts = firstName.split(' ')
            firstName = ' '.join(nameParts[0:3]) + '…'

        return m.group(1) + firstName + ' e outros(as)' + m.group(3)

    if (len(firstName) > 20):
        nameParts = firstName.split(' ')
        firstName = ' '.join(nameParts[0:3]) + '…'

    return m.group(1) + firstName + m.group(3)


def truncLongName(text):
    if (len(text) < 280):
        return text # no mods needed

    newText = re.sub(r"(de autoria de )(.*)(, fala sobre)", repNameV1, text)

    # try again with without "e outros...")
    if (len(newText) > 280):
        newText = re.sub(r"(de autoria de )(.*)(, fala sobre)", repNameV2, text)

    # if still too long, remove a lot of info
    if (len(newText) > 280):
        newText = re.sub(r"de autoria de.*sofreu alterações em sua tramitação\. ", '', text)

    if (len(newText) > 280):
        newText = newText.replace("fala sobre o tema", "fala sobre")

    if (len(newText) > 280):
        newText = newText.replace("e sofreu alterações em sua tramitação", "teve alterações na tramitação")

    if (len(newText) > 280):
        newText = text.replace('🕙', '').replace('↪️', '').replace('🔗', '').replace('🔈', '')

    if (len(newText) > 280):
        newText = text.replace('\n', '')

    return newText
